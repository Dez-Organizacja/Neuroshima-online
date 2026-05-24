// src/images.ts

const modules = import.meta.glob(
  "./assets/{borgo,hegemonia,moloch,posterunek,inne}/*.{png,jpg,jpeg}",
  {
    eager: true,
  }
)

export const imagesByName: Record<string, string> =
  Object.fromEntries(
    Object.entries(modules).map(
      ([path, module]: any) => {
        // example:
        // ./assets/cards/card1.png

        const key = path
          .replace("./assets/", "")
          .replace(/\.[^/.]+$/, "")

        // result:
        // cards/card1

        return [key, module.default]
      }
    )
  )

console.log(imagesByName)