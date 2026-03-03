-- Options are automatically loaded before lazy.nvim startup
-- Default options that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/options.lua
-- Add any additional options here

local opt = vim.opt
local g = vim.g

opt.guifont = "monospace:h16" -- Set gui font
opt.swapfile = false -- Disable swap file
opt.showcmd = false -- Disable command in lualine
opt.foldlevel = 99
opt.foldlevelstart = 99

-- Enable this option to avoid conflicts with Prettier.
g.lazyvim_prettier_needs_config = true

vim.filetype.add({
  extension = {
    env = "sh",
  },
  filename = {
    [".env"] = "sh",
  },
  pattern = {
    ["%.env%.[%w_.-]+"] = "sh",
  },
})
