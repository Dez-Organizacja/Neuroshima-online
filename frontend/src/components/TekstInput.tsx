type TextInputProps = {
    value: string;
    className? : string;
    onChange: (newValue: string) => void;
    placeholder?: string;
};

export default function TextInput({
    value,
    className,
    onChange,
    placeholder,
}: TextInputProps) {
    return (
        <input
            className={className}
            type = "text"
            value = {value}
            onChange={(event) => onChange(event.target.value)}
            placeholder = {placeholder}
        />
    )
}