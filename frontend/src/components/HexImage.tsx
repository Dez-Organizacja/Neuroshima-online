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
            transform: `rotate(${rotation}deg) scale(1)`,
        }}
        />
    )
}