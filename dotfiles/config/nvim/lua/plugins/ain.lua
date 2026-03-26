return {
  "jonaslu/ain",
  lazy = false,
  config = function()
    local path = vim.fn.stdpath("data") .. "/lazy/ain/grammars/vim"
    vim.opt.rtp:append(path)

    vim.filetype.add({
      extension = { ain = "ain" },
    })
  end,
}
