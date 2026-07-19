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
                    b.pos.x = b.pos.x + b.vel.x * delta;
                    b.pos.y = b.pos.y + b.vel.y * delta;
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
                contacts: this.manifold.contacts
            };

            this.historicBuffer.push(newState);
            return newState;
        }
    }
    


