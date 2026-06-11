return {
  {
    "stevearc/conform.nvim",
    opts = function()
      -- local plugin = require("lazy.core.config").plugins["conform.nvim"]
      -- if plugin.config ~= M.setup then
      --   LazyVim.error({
      --     "Don't set `plugin.config` for `conform.nvim`.\n",
      --     "This will break **LazyVim** formatting.\n",
      --     "Please refer to the docs at https://www.lazyvim.org/plugins/formatting",
      --   }, { title = "LazyVim" })
      -- end
      ---@type conform.setupOpts
      local opts = {
        default_format_opts = {
          timeout_ms = 3000,
          async = false, -- not recommended to change
          quiet = false, -- not recommended to change
          lsp_format = "fallback", -- not recommended to change
        },
        formatters_by_ft = {
          lua = { "stylua" },
          fish = { "fish_indent" },
          sh = { "shfmt" },
          -- http = { "kulala" },
          -- rest = { "kulala" },
        },
      }
      return opts
    end,
  },
}
