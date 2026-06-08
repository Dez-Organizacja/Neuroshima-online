import type { KeyboardEventHandler } from "react";

type TextInputProps = {
  value: string;
  className?: string;
  onChange: (newValue: string) => void;
  placeholder?: string;
  type?: "text" | "password" | "email";
  id?: string;
  name?: string;
  autoComplete?: string;
  disabled?: boolean;
  onKeyDown?: KeyboardEventHandler<HTMLInputElement>;
  ariaLabel?: string;
};

export default function TextInput({
  value,
  className,
  onChange,
  placeholder,
  type = "text",
  id,
  name,
  autoComplete,
  disabled = false,
  onKeyDown,
  ariaLabel,
}: TextInputProps) {
  return (
    <input
      id={id}
      name={name}
      className={className}
      type={type}
      value={value}
      onChange={(event) => onChange(event.target.value)}
      placeholder={placeholder}
      autoComplete={autoComplete}
      disabled={disabled}
      onKeyDown={onKeyDown}
      aria-label={ariaLabel}
    />
  );
}