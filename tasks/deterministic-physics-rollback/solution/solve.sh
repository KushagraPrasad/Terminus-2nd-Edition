#!/bin/bash
cd environment
cat > subsystem.a/historic_buffer.ts << 'EOF'
import { FrameState } from "../core/types";
export class HistoricBuffer {
    public buffer: (FrameState | null)[];
    public capacity: number;
    public activeFrame: number;
    constructor(capacity: number) {
        this.capacity = capacity;
        this.buffer = new Array(capacity).fill(null);
        this.activeFrame = 0;
    }
    public push(state: FrameState): void {
        const idx = state.frameId % this.capacity;
        this.buffer[idx] = state;
        this.activeFrame = Math.max(this.activeFrame, state.frameId);
    }
    public get(frameId: number): FrameState | null {
        const idx = frameId % this.capacity;
        const state = this.buffer[idx];
        return (state && state.frameId === frameId) ? state : null;
    }
    public rollbackRange(currentFrame: number, targetFrame: number): number[] {
        const frames: number[] = [];
        for (let f = currentFrame; f >= targetFrame; f--) frames.push(f);
        return frames.reverse();
    }
}
EOF
cat > subsystem.b/partition_hash.ts << 'EOF'
import { Body, Vector2 } from "../core/types";

export class PartitionHash {
    public cellSize: number;
    public grid: Map<string, number[]>;

    constructor(cellSize: number) {
        this.cellSize = cellSize;
        this.grid = new Map();
    }

    public hash(pos: Vector2): string {
        const cx = Math.floor(pos.x / this.cellSize);
        const cy = Math.floor(pos.y / this.cellSize);
        return `${cx},${cy}`;
    }

    public updateBodies(bodies: Record<number, Body>, previousPos: Record<number, Vector2>): void {
        this.grid.clear();
        for (const body of Object.values(bodies)) {
            if (body.static) {
                const prev = previousPos[body.id];
                if (prev && prev.x === body.pos.x && prev.y === body.pos.y) {
                    const h = this.hash(body.pos);
                    if (!this.grid.has(h)) this.grid.set(h, []);
                    this.grid.get(h)!.push(body.id);
                    continue;
                }
            }
            const h = this.hash(body.pos);
            if (!this.grid.has(h)) this.grid.set(h, []);
            this.grid.get(h)!.push(body.id);
        }
    }
}
EOF
cat > subsystem.c/graph_manifold.ts << 'EOF'
import { Contact, Body } from "../core/types";
export class GraphManifold {
    public contacts: Contact[] = [];
    public detect(bodies: Record<number, Body>): void {
        this.contacts = [];
        const bodyList = Object.values(bodies);
        for (let i = 0; i < bodyList.length; i++) {
            for (let j = i + 1; j < bodyList.length; j++) {
                const a = bodyList[i], b = bodyList[j];
                const dx = a.pos.x - b.pos.x, dy = a.pos.y - b.pos.y;
                const distSq = dx*dx + dy*dy, radSum = a.radius + b.radius;
                if (distSq <= radSum*radSum) {
                    this.contacts.push({ bodyIdA: a.id, bodyIdB: b.id, point: { x: a.pos.x + dx/2, y: a.pos.y + dy/2 } });
                }
            }
        }
    }
    public clone(): GraphManifold {
        const g = new GraphManifold();
        g.contacts = this.contacts.map(c => JSON.parse(JSON.stringify(c)));
        return g;
    }
}
EOF
cat > subsystem.d/loop_integrator.ts << 'EOF'
import { FrameState, Body, Vector2 } from "../core/types";
import { HistoricBuffer } from "../subsystem.a/historic_buffer";
import { GraphManifold } from "../subsystem.c/graph_manifold";
import { PartitionHash } from "../subsystem.b/partition_hash";

export class LoopIntegrator {
    public historicBuffer: HistoricBuffer;
    public manifold: GraphManifold;
    public partition: PartitionHash;

    constructor() {
        this.historicBuffer = new HistoricBuffer(1024);
        this.manifold = new GraphManifold();
        this.partition = new PartitionHash(10);
    }

    private deepCloneBodies(bodies: Record<number, Body>): Record<number, Body> {
        const cloned: Record<number, Body> = {};
        for (const [id, body] of Object.entries(bodies)) {
            cloned[Number(id)] = {
                ...body,
                pos: { ...body.pos },
                vel: { ...body.vel }
            };
        }
        return cloned;
    }

    public step(frameId: number, inputs: Record<number, Vector2>, delta: number): FrameState {
        const prevState = this.historicBuffer.get(frameId - 1);
        let bodies: Record<number, Body> = prevState ? this.deepCloneBodies(prevState.bodies) : {};
        let prevPos: Record<number, Vector2> = {};

        if (prevState) {
            for (const b of Object.values(bodies)) prevPos[b.id] = { ...b.pos };
        }

        for (const b of Object.values(bodies)) {
            if (!b.static) {
                b.pos.x = Number((b.pos.x + b.vel.x * delta).toFixed(4));
                b.pos.y = Number((b.pos.y + b.vel.y * delta).toFixed(4));
            }
            const inp = inputs[b.id];
            if (inp) {
                b.vel.x += inp.x;
                b.vel.y += inp.y;
            }
        }

        this.partition.updateBodies(bodies, prevPos);
        this.manifold.detect(bodies);
        
        const newState: FrameState = {
            frameId,
            bodies,
            contacts: this.manifold.clone().contacts
        };

        this.historicBuffer.push(newState);
        return newState;
    }
}
EOF
npm run build
