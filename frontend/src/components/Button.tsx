import type { ReactNode } from "react";
import { CSSProperties } from "react";

type ButtonProps = {
    className? : string
    text : ReactNode;
    onClick? : () => void;
    // style?: CSSProperties;
};

export default function Button({
    className,
    // style,
    text,
    onClick, 
}:ButtonProps){
    return <button className={className}
        // style={style}
    type="button" onClick={onClick}>
        {text}
    </button>
}