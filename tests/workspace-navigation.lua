-- Run from the repository root with lua tests/workspace-navigation.lua.
local callbacks, removed = {}, {}
local active, target
hl = {
  unbind = function(key) removed[key] = true end,
  get_active_workspace = function() return { id = active } end,
  dispatch = function(value) target = tonumber(value.workspace) end,
  dsp = { focus = function(value) return value end },
}
o = { bind = function(key, description, callback) callbacks[key] = callback end }
dofile((arg[1] or ".") .. "/hypr/bindings.lua")
for _, pair in ipairs({
  { "SUPER + TAB", 1 }, { "SUPER + SHIFT + TAB", -1 },
  { "SUPER + mouse_down", 1 }, { "SUPER + mouse_up", -1 },
}) do
  assert(removed[pair[1]])
  for id = 1, 10 do
    active = id
    callbacks[pair[1]]()
    assert(target == ((id - 1 + pair[2]) % 10) + 1)
  end
  active = -1
  callbacks[pair[1]]()
  assert(target == (pair[2] > 0 and 1 or 10))
end
print("PASS ten-workspace keyboard/mouse navigation and wraparound")
