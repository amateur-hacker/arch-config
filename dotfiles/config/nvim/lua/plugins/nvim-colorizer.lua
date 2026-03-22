return {
  "NvChad/nvim-colorizer.lua",
  -- ft = { "html", "css", "scss", "javascriptreact", "typescriptreact", "astro" },
  event = { "BufReadPost", "BufNewFile" },
  opts = {
    user_default_options = {
      tailwind = true,
      RRGGBBAA = true,
      AARRGGBB = true,
      rgb_fn = true,
      hsl_fn = true,
      css = true,
      css_fn = true,
      names = false,
    },
  },
}
