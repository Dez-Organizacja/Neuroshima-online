import React from "react";
import "./Hexagon.css";

type HexagonProps = {
    x: number;
    y: number;
    poz1?: number;
    poz2?: number;
    size?: number;
    color?: string;
    rotation?: number;
    onClick?: () => void;
    children?: React.ReactNode;
};

const Hexagon: React.FC<HexagonProps> = ({
    x,
    y,
    poz1,
    poz2,
    size = 100,
    color = "#4CAF50",
    rotation = 0,
    onClick,
    children,
}) => {
    const height = size * 0.866;

    return (
        <div
            className="hexagon"
            // onClick={onClick}
            onClick={() => console.log("Clicked hex:", { poz1, poz2 })}
        style={{
            width: size,
            height: height,
            backgroundColor: color + "33",
            position: "absolute",
            left: x - (size / 2),
            top: y - (height / 2),
            transform: `rotate(${rotation}deg) scale(1)`,
        }}
        >
        < div className="hexagon-content">{children}</div>
         </div>
    );
};

export default Hexagon;