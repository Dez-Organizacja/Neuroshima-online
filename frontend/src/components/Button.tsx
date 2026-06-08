import type { ReactNode } from "react";

type ButtonProps = {
  className?: string;
  text: ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  ariaPressed?: boolean;
};

export default function Button({
  className,
  text,
  onClick,
  disabled = false,
  ariaPressed,
}: ButtonProps) {
  return (
    <button
      className={className}
      type="button"
      onClick={onClick}
      disabled={disabled}
      aria-pressed={ariaPressed}
    >
      {text}
    </button>
  );
}
