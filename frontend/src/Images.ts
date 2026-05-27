const modules = import.meta.glob<{ default: string }>(
  "/src/assets/{borgo,hegemonia,moloch,posterunek,inne}/*.{png,jpg,jpeg}",
  {
    eager: true,
  }
)

export const imagesByName: Record<string, string> = Object.fromEntries(
  Object.entries(modules).map(([path, module]) => {
    const key = path
      .replace("/src/assets/", "")
      .replace(/\.[^.]+$/, "")

    return [key, module.default]
  })
)