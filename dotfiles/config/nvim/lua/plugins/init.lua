return {
  {
    "akinsho/bufferline.nvim",
    -- TODO: Remove this once https://github.com/LazyVim/LazyVim/pull/6354 is merged
    -- init = function()
    --   local bufline = require("catppuccin.groups.integrations.bufferline")
    --   function bufline.get()
    --     return bufline.get_theme()
    --   end
    -- end,
    opts = function(_, opts)
      table.insert(opts.options.offsets, {
        filetype = "snacks_layout_box",
        separator = true,
      })
      table.insert(opts.options.offsets, {
        filetype = "NvimTree",
        separator = true,
      })
    end,
  },
  -- TODO: Remove this once https://github.com/LazyVim/LazyVim/pull/6354 is merged
  -- {
  --   "catppuccin/nvim",
  --   opts = function(_, opts)
  --     local module = require("catppuccin.groups.integrations.bufferline")
  --     if module then
  --       module.get = module.get_theme
  --     end
  --     return opts
  --   end,
  -- },
  {
    "neovim/nvim-lspconfig",
    opts = {
      servers = {
        html = {},
        emmet_ls = {},
        cssls = {
          settings = {
            css = {
              validate = true,
              lint = {
                unknownAtRules = "ignore",
              },
            },
          },
        },
      },
    },
  },
  {
    "folke/snacks.nvim",
    keys = {
      { "<leader>fe", false },
      { "<leader>fE", false },
      { "<leader>e", false },
      { "<leader>E", false },
    },
    opts = {
      explorer = { enabled = false },
    },
  },
  {
    "nvim-lualine/lualine.nvim",
    opts = {
      options = {
        section_separators = { left = "", right = "" },
        component_separators = { left = "", right = "" },
      },
      extensions = { "trouble", "lazy", "nvim-tree", "man", "mason", "fzf" },
    },
  },
  {
    "saghen/blink.cmp",
    version = "1.*",
    opts = {
      keymap = {
        ["<c-j>"] = { "select_next" },
        ["<c-k>"] = { "select_prev" },
      },
    },
  },
  {
    "nvim-mini/mini.icons",
    opts = {
      default = {
        file = { glyph = "" },
      },
    },
  },
  -- {
  --   "saghen/blink.cmp",
  --   dependencies = {
  --     {
  --       "Exafunction/windsurf.nvim",
  --     },
  --   },
  --   opts = {
  --     sources = {
  --       default = { "lsp", "path", "snippets", "buffer", "codeium" },
  --       providers = {
  --         codeium = { name = "Codeium", module = "codeium.blink", async = true },
  --       },
  --     },
  --   },
  -- },
  -- {
  --   "Exafunction/windsurf.nvim",
  --   dependencies = {
  --     "nvim-lua/plenary.nvim",
  --     "saghen/blink.cmp",
  --   },
  --   config = function()
  --     require("codeium").setup({
  --       virtual_text = {
  --         enabled = true,
  --       },
  --       default_filetype_enabled = true,
  --       filetypes = {
  --         html = true,
  --         typescript = true,
  --         javascript = true,
  --         css = true,
  --         json = true,
  --         java = true,
  --       },
  --     })
  --   end,
  -- },
  -- {
  --   "echasnovski/mini.files",
  --   keys = {
  --     -- { "<leader>e", "<leader>fm", desc = "Open min.files (Directory of Current File)", remap = true },
  --     -- { "<leader>E", "<leader>fM", desc = "Open mini.files (cwd)", remap = true },
  --   },
  --   opts = {
  --     options = {
  --       use_as_default_explorer = false,
  --     },
  --   },
  -- },

  {
    "folke/noice.nvim",
    opts = function(_, opts)
      table.insert(opts.routes, {
        filter = {
          event = "notify",
          find = "No information available",
        },
        opts = { skip = true },
      })

      opts.commands = {
        all = {
          -- options for the message history that you get with `:Noice`
          view = "split",
          opts = { enter = true, format = "details" },
          filter = {},
        },
      }

      vim.api.nvim_create_autocmd("FileType", {
        pattern = "markdown",
        callback = function(event)
          vim.schedule(function()
            require("noice.text.markdown").keys(event.buf)
          end)
        end,
      })

      opts.presets.lsp_doc_border = true
    end,
  },
  {
    "nvim-neo-tree/neo-tree.nvim",
    enabled = false,
  },
  {
    "jonaslu/ain",
    dir = vim.fn.stdpath("data") .. "/lazy/ain/grammars/vim",
  },
  {
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
  },
  {
    "catppuccin/nvim",
    opts = {
      color_overrides = {
        mocha = {
          blue = "#b4befe", -- lavender
        },
      },
    },
  },
  {
    "sahaj-b/brainrot.nvim",
    dependencies = { "3rd/image.nvim" },
    -- event = "VeryLazy",
    lazy = true,
    opts = {
      -- defaults:

      disable_phonk = false, -- skip phonk/overlay on "no errors"
      phonk_time = 2.5, -- seconds the phonk/image overlay stays
      min_error_duration = 0.5, -- minimum seconds errors must exist before phonk triggers (0 = instant)
      block_input = true, -- block input during phonk/overlay
      dim_level = 60, -- phonk overlay darkness 0..100

      sound_enabled = true, -- enable sounds
      image_enabled = true, -- enable images (needs image.nvim)

      boom_volume = 50, -- volume for vine boom sound (0..100)
      phonk_volume = 50, -- volume for phonk sound (0..100)

      boom_sound = nil, -- custom boom sound path (e.g., "~/sounds/boom.ogg")
      phonk_dir = nil, -- custom phonk folder path (e.g., "~/sounds/phonks")
      image_dir = nil, -- custom image folder path (e.g., "~/memes/images")

      lsp_wide = false, -- track errors workspace-wide(get ALL lsp errors)
    },
  },
  {
    "3rd/image.nvim",
    build = false, -- so that it doesn't build the rock https://github.com/3rd/image.nvim/issues/91#issuecomment-2453430239
    opts = {
      processor = "magick_cli",
    },
  },
}
