import React from "react"
import { useRef, useState, useEffect } from "react"
import "./HexImage.css"
import { imagesByName } from "./../Images"
import { GameState } from "../Dlaigora"

type ImageProps = {
    imageName: string
    x: number
    y: number
    poz1: number
    poz2: number
    height: number
    rotation: number
    gameState: GameState
}

export default function Image({ 
    imageName,
    x,
    y,
    poz1,
    poz2,
    height,
    rotation,
    gameState,
}: ImageProps) {
    const imageSrc = imagesByName[imageName]

    const imageRef = useRef<HTMLImageElement>(null);
    const [width, setWidth] = useState(0);

    useEffect(() => {
        if (!imageRef.current) return

        const observer = new ResizeObserver(() => {
            if (imageRef.current) {
                setWidth(
                    imageRef.current.offsetWidth
                )
            }
        })

        observer.observe(imageRef.current)

        return () => {
            observer.disconnect()
        }
    }, [])


    const canRotate = gameState.view.uiState.mode === "rotation";
    const [Rotation, setRotation] = useState(rotation);
    useEffect(() => {

        const handleKeyDown = (event: KeyboardEvent) => {
            if(!canRotate) return;
            const field = gameState.view.availableActions.board.find(field =>
                field[0] === poz1 &&
                field[1] === poz2
            );
            if(!field) return;
            console.log("hjgjh");

            if (event.key === "ArrowLeft") {
                setRotation(prev => (prev + 300) % 360);
            }

            if (event.key === "ArrowRight") {
                setRotation(prev => (prev + 60) % 360);
            }
        };

        window.addEventListener("keydown", handleKeyDown);

        return () => {
            window.removeEventListener("keydown", handleKeyDown);
        };

    }, [canRotate]);

    return (
        <img
        ref={imageRef}
        src={imageSrc}
        alt={imageName}
        className="placed-image"

        onLoad={() => {
            if (imageRef.current) {
                setWidth(imageRef.current.offsetWidth)
            }
        }}

        style={{
            height: height,
            width: "auto",
            left: x - (width / 2),
            top: y - (height / 2),
            transform: `rotate(${Rotation}deg) scale(1)`,
        }}
        />
    )
}