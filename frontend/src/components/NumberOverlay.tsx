import "./NumberOverlay.css";

type NumberOverlayProps = {
    x: number;
    y: number;
    value: number;
    opacity?: number;
    height: number,
};

export default function NumberOverlay({
    x,
    y,
    value,
    opacity=1,
    height,
}: NumberOverlayProps) {
    return (
        <div
            className="number-overlay"
            style={{
                left: x,
                top: y,
                opacity: opacity,
                fontSize: height,
                lineHeight: "1",
            }}
        >
            {value}
        </div>
    );
}