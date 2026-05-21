import React from "react"
import { useRef, useState, useEffect } from "react"
import "./HexImage.css"
import { imagesByName } from "./../Images"

type ImageProps = {
    imageName: string
    x: number
    y: number
    height: number
    rotation: number
}

export default function Image({ 
    imageName,
    x,
    y,
    height,
    rotation,
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