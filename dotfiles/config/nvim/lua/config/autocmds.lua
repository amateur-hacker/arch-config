-- Autocmds are automatically loaded on the VeryLazy event
-- Default autocmds that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/autocmds.lua
--
-- Add any additional autocmds here
-- with `vim.api.nvim_create_autocmd`
--
-- Or remove existing autocmds by their group name (which is prefixed with `lazyvim_` for the defaults)
-- e.g. vim.api.nvim_del_augroup_by_name("lazyvim_wrap_spell")

local function augroup(name)
  return vim.api.nvim_create_augroup(name, { clear = true })
end -- Create/get autocommand group
local autocmd = vim.api.nvim_create_autocmd -- Create autocommand

-- Trim trailing whitespace on save
autocmd("BufWritePre", {
  group = augroup("trim_whitespace"),
  callback = function()
    vim.cmd([[silent! %s/\s\+$//e]])
  end,
})

-- Disable auto-commenting on new lines
autocmd("BufEnter", {
  group = augroup("auto_commenting_off"),
  callback = function()
    vim.opt_local.formatoptions:remove({ "c", "r", "o" })
  end,
})

-- Auto open nvim-tree when opening a directory with lazy loading support
autocmd("VimEnter", {
  group = augroup("auto_open_nvim_tree"),
  callback = function()
    local args = vim.fn.argv()
    local arg = args[1]
    if arg ~= "" and vim.fn.isdirectory(arg) == 1 then
      vim.cmd.cd(arg)

      require("lazy").load({ plugins = { "nvim-tree.lua" } })

      vim.cmd("NvimTreeToggle")
    end
  end,
})
