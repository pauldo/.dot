return {
  {
    "folke/snacks.nvim",
    opts = {
      dashboard = {
        preset = {
          -- https://rakko.tools/zh-cn/tools/ascii-art-generator
          header = [[
██▄  ▄██  ▄▄▄ ▄▄▄▄▄▄ ▄▄▄▄  ▄▄ ▄▄ ▄▄   ███  ██ ▄▄▄▄▄  ▄▄▄  
██ ▀▀ ██ ██▀██  ██   ██▄█▄ ██ ▀█▄█▀   ██ ▀▄██ ██▄▄  ██▀██ 
██    ██ ██▀██  ██   ██ ██ ██ ██ ██   ██   ██ ██▄▄▄ ▀███▀ 
 ]],
        },
      },
      picker = {
        hidden = true,
        ignored = true,

        sources = {
          files = {
            hidden = true,
            ignored = true,
          },
          explorer = {
            hidden = true,
            ignored = true,
          },
          grep = {
            hidden = true,
            ignored = true,
          },
        },
        exclude = {
          ".git",
          ".DS_Store",
        },
      },
    },
  },
}
