import React from "react"
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

    return (
        <img
        src={imageSrc}
        alt={imageName}
        className="placed-image"
        style={{
            left: `${x}px`,
            top: `${y}px`,
            height: `${height}px`,
            transform: `rotate(${rotation}deg) scale(1)`,
        }}
        />
    )
}

// export default function App() {
//   return (
//     <div className="canvas">
//       <MyImage
//         x={300}
//         y={150}
//         height={200}
//         rotation={30}
//       />

//       <MyImage
//         x={500}
//         y={250}
//         height={120}
//         rotation={-15}
//       />
//     </div>
//   )
// }