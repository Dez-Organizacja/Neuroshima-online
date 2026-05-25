type Props = {
  strings: string[];
};

export default function StringList({ strings }: Props) {
  return (
    <div>
      {strings.map((text, index) => (
        <p key={index}>{text}</p>
      ))}
    </div>
  );
}