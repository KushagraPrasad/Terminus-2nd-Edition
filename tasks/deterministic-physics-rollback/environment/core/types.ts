export interface Vector2 {
        x: number;
        y: number;
    }
    export interface Body {
        id: number;
        pos: Vector2;
        vel: Vector2;
        static: boolean;
        radius: number;
    }
    export interface Contact {
        bodyIdA: number;
        bodyIdB: number;
        point: Vector2;
    }
    export interface FrameState {
        frameId: number;
        bodies: Record<number, Body>;
        contacts: Contact[];
    }
    
