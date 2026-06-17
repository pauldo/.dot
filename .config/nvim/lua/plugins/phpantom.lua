return {
  {
    "neovim/nvim-lspconfig",
    opts = {
      -- 1. 显式禁用默认的 intelephense
      servers = {
        intelephense = {
          enabled = false,
        },
        -- 2. 注册并启用 phpantom
        phpantom_lsp = {
          enabled = true,
          -- 如果你的系统 PATH 中能直接找到 phpantom_lsp 编译产物，下面这行可以不写。
          -- 如果你使用的是独立下载的二进制文件，可以显式指定绝对路径：
          -- cmd = { "/home/cheems/.cargo/bin/phpantom_lsp" },

          filetypes = { "php" },
          root_markers = { "composer.json", ".git" },
        },
      },
      -- 3. 阻止 Mason 自动去下载 intelephense
      setup = {
        intelephense = function()
          return true -- 返回 true 代表跳过默认的初始化设置
        end,
      },
    },
  },
}
