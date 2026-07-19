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
            if (state && state.frameId === frameId) return state;
            return null;
        }

        public rollbackRange(currentFrame: number, targetFrame: number): number[] {
            const frames: number[] = [];
            for (let f = currentFrame; f > targetFrame; f--) {
                frames.push(f);
            }
            return frames.reverse();
        }
    }
    


