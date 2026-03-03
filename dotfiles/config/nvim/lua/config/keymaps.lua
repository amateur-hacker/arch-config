-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here

-- Change leader and local leader to Space
local map = vim.keymap

-- Disable arrow keys
map.set("", "<up>", "<nop>")
map.set("", "<down>", "<nop>")
map.set("", "<left>", "<nop>")
map.set("", "<right>", "<nop>")

-- Disable <C-k>
map.set("i", "<C-k>", "<nop>")

-- Delete single character without copying into register
map.set("n", "x", '"_x')

-- Paste without losing the contents of the register
map.set({ "v", "x" }, "p", '"_dP')

-- Increment/Decrement number
map.set("n", "=", "<C-a>", { desc = "Increment by 1", remap = true })
map.set("n", "-", "<C-x>", { desc = "Decrement by 1", remap = true })

-- Copy file
map.set("n", "<leader>y", "<cmd>%y+<cr>", { desc = "Copy whole File" })

-- Save file
map.del({ "i", "x", "n", "s" }, "<c-s>")
map.set("n", "<leader><leader>", "<cmd>silent write<cr><esc>", { desc = "Save File" })

-- Toggle inlay hints
map.set("n", "<leader>i", function()
  local bufnr = 0
  local enabled = vim.lsp.inlay_hint.is_enabled({ bufnr = bufnr }) or false
  vim.lsp.inlay_hint.enable(not enabled, { bufnr = bufnr })
  -- vim.lsp.inlay_hint.enable(not vim.lsp.inlay_hint.is_enabled())
end, { desc = "Toggle Inlay Hints" })

-- Open mason
map.set("n", "<leader>m", "<cmd>Mason<cr>", { desc = "Open Mason" })

-- Custom buffer mappings
map.set("n", "Q", function()
  Snacks.bufdelete()
end, { desc = "Delete Buffer" })
map.set("n", "<c-s-]>", "<cmd>BufferLineMoveNext<cr>", { desc = "Move Buffer Right" })
map.set("n", "<c-s-[>", "<cmd>BufferLineMovePrev<cr>", { desc = "Move Buffer Left" })
map.set("n", "<leader>b.", "<cmd>BufferLineMoveNext<cr>", { desc = "Move Buffer Right" })
map.set("n", "<leader>b,", "<cmd>BufferLineMovePrev<cr>", { desc = "Move Buffer Left" })
