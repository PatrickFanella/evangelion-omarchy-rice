local profiles = {
  ["violet"] = { accent = "#B69CFF", selection = "#4C2F99", muted = "#6A5A8C" },
  subcult = { accent = "#00FF88", selection = "#3B2470", muted = "#5E5570" },
  engineering = { accent = "#F28C28", selection = "#633417", muted = "#806752" },
  ["acid"] = { accent = "#00FF88", selection = "#0F4A33", muted = "#4E6B5E" },
  ["paper"] = { accent = "#F0ECE4", selection = "#4A4033", muted = "#7A7064" },
  ["ink"] = { accent = "#A78BFA", selection = "#2E2448", muted = "#55506A" },
}

local function profile_path()
  local state_home = vim.env.XDG_STATE_HOME or (vim.env.HOME .. "/.local/state")
  return state_home .. "/subcult-rice/terminal-profile"
end

local function apply_profile()
  local file = io.open(profile_path(), "r")
  local name = file and file:read("*l") or "violet"
  if file then
    file:close()
  end

  local colors = profiles[name] or profiles["violet"]
  vim.api.nvim_set_hl(0, "Visual", { bg = colors.selection })
  vim.api.nvim_set_hl(0, "CursorLineNr", { fg = colors.accent, bold = true })
  vim.api.nvim_set_hl(0, "FloatBorder", { fg = colors.accent })
  vim.api.nvim_set_hl(0, "TelescopeSelection", { bg = colors.selection, bold = true })
  vim.api.nvim_set_hl(0, "TelescopeBorder", { fg = colors.muted })
  vim.api.nvim_set_hl(0, "SnacksPickerListCursorLine", { bg = colors.selection })
  vim.api.nvim_set_hl(0, "SnacksPickerBorder", { fg = colors.muted })
end

return {
  {
    name = "subcult-terminal-profile",
    dir = vim.fn.stdpath("config"),
    lazy = false,
    priority = 900,
    config = function()
      vim.api.nvim_create_autocmd({ "ColorScheme", "FocusGained", "VimEnter" }, {
        callback = function()
          vim.schedule(apply_profile)
        end,
      })
      apply_profile()
    end,
  },
}
