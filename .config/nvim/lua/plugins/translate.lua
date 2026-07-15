return {
  {
    "potamides/pantran.nvim",
    opts = {
      default_engine = "google",
      engines = {
        google = {
          fallback = {
            default_target = "zh",
          },
        },
      },
    },
    keys = {
      { "<leader>ts", "y<cmd>Pantran<cr>p", mode = { "n", "x" }, desc = "Pantran 翻译" },
      { "<leader>tt", "yy<cmd>Pantran<cr>p", mode = "n", remap = true, desc = "翻译当前行" },
    },
  },
}
