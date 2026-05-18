// src/images.ts

const modules = import.meta.glob(
  "./assets/borgo/*.{png,jpg,jpeg}",
  {
    eager: true,
  }
)

console.log(modules)

export const imagesByName: Record<string, string> =
  Object.fromEntries(
    Object.entries(modules).map(
      ([path, module]: any) => {
        const fileName =
          path.split("/").pop() as string

        const name =
          fileName.replace(/\.[^/.]+$/, "")

        return [name, module.default]
      }
    )
  )

console.log(imagesByName)
console.log(Object.keys(imagesByName))