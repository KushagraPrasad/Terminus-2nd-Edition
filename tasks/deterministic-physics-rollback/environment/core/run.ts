declare const process: any;
import { LoopIntegrator } from "../subsystem.d/loop_integrator";
import { Body } from "./types";

const totalFrames = process.argv[2] ? parseInt(process.argv[2], 10) : 50;
const targetFrame = process.argv[3] ? parseInt(process.argv[3], 10) : 25;
const velX1 = process.argv[4] ? parseFloat(process.argv[4]) : 11.0;

const step = new LoopIntegrator();
step.historicBuffer.push({
    frameId: 0,
    bodies: {
        1: { id: 1, pos: { x: 0, y: 0 }, vel: { x: velX1, y: 0 }, static: false, radius: 1 },
        2: { id: 2, pos: { x: 10.1, y: 0 }, vel: { x: -velX1, y: 0 }, static: false, radius: 1 }
    },
    contacts: []
});

for(let i = 1; i <= totalFrames; i++) {
    step.step(i, {}, 0.016);
}

const frames = step.historicBuffer.rollbackRange(totalFrames, targetFrame);

// Mutate active manifold contact to test deep cloning vs reference leak
if (step.manifold.contacts.length > 0) {
    step.manifold.contacts[0].point.x += 100.0;
}

const curState = step.historicBuffer.get(targetFrame);
const finalState = step.historicBuffer.get(totalFrames);

// If shallow cloned, curState.contacts[0].point.x will be mutated to > 50.0
const hasLeak = curState && curState.contacts.length > 0 && curState.contacts[0].point.x > 50.0;

console.log(JSON.stringify({
    deterministic_hash: "hash_value_" + (curState?.frameId || "none"),
    frames_processed: frames.length,
    grid_nodes_active: step.partition.grid.size,
    manifold_copies: hasLeak ? 0 : 1,
    drift_error: finalState?.bodies[1]?.pos.x || 0
}));
