type DisplayTextProps = {
    text : string;
    className? : string;
};

export default function DisplayText({
    text,
    className,
}:DisplayTextProps){
    return <p className={className}>{text}</p>
}