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
    


