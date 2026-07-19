import { Contact, Body, Vector2 } from "../core/types";

    export class GraphManifold {
        public contacts: Contact[] = [];
        
        public detect(bodies: Record<number, Body>): void {
            this.contacts = [];
            const bodyList = Object.values(bodies);
            for (let i = 0; i < bodyList.length; i++) {
                for (let j = i + 1; j < bodyList.length; j++) {
                    const a = bodyList[i];
                    const b = bodyList[j];
                    const dx = a.pos.x - b.pos.x;
                    const dy = a.pos.y - b.pos.y;
                    const distSq = dx*dx + dy*dy;
                    const radSum = a.radius + b.radius;
                    if (distSq <= radSum*radSum) {
                        this.contacts.push({ bodyIdA: a.id, bodyIdB: b.id, point: { x: a.pos.x + dx/2, y: a.pos.y + dy/2 } });
                    }
                }
            }
        }

        public clone(): GraphManifold {
            const g = new GraphManifold();
            g.contacts = [...this.contacts];
            return g;
        }
    }
    


