# Console smoke check

Run `python -m bmi_explorer --no-banner` in the installed environment and paste:

```python
n = 'uniform_2d__slope'
u = bmi.get_var_grid(n)
r = bmi.get_var_grid('rectilinear_2d__precip_rate')
p = bmi.get_var_grid('points_2d__snow_depth')
original = bmi
bmi.get_grid_shape(u, np.empty(2, dtype=np.int32))
bmi.get_grid_x(r, np.empty(4, dtype=np.float64))
bmi.get_grid_x(p, np.empty(6, dtype=np.float64))
bmi.set_value(n, [1.0])
print('recovered', bmi.get_current_time())
print('same model', bmi is original, 'grids', len(explorer.list()))
print(bmi.get_grid_rank(bmi.get_var_grid('scalar__velocity')))
print(explorer.topology(bmi.get_var_grid('unstructured_mixed__depth')))
exit()
```

Expected significant output (traceback paths and prompts vary):

```text
array([3, 4], dtype=int32)
array([100., 102., 107., 115.])
array([ 0.,  2.,  3.,  1., -1.,  1.])
BMITypeError: set_value('uniform_2d__slope') expected ...
recovered 0.0
same model True grids 9
0
grid 8: nodes=6, edges=8, faces=3
face 0: nodes=[1, 2, 3, 5], edges=[1, 2, 6, 5]
face 1: nodes=[3, 4, 0, 5], edges=[3, 4, 7, 6]
face 2: nodes=[0, 1, 5], edges=[0, 5, 7]
```

Automated subprocess tests cover error recovery, multiline Python, comparisons
without model replacement, installed module/script launch outside the checkout,
and clean exit/EOF. `--list` prints all nine grids. `--tour grids` shows a valid
uniform-spacing call and a failing rectilinear-spacing call on the same model.


## Terminal editing and help

Launch `.conda/bin/python -m bmi_explorer` in a terminal. Check that the banner
shows `all_grids`, readable grid/variable rows, and runnable learning examples.

1. Type `bmi.get_current_t`, then Tab: it should complete the method name. Add
   `)` if needed, then Enter; the initial time is `0.0`.
2. Type `bmi.get_var_grid('uniform_2d`, then Tab: it should offer
   `uniform_2d__slope`. Close the quote and parenthesis, then Enter.
3. Run `help(bmi.get_value)`. Documentation appears in scrollback and the `>>>`
   prompt returns immediately. Run `print('after help')`; no stale pager remains.
4. Run `print(help_bmi('get_value'))`; teaching sections use real line breaks.
5. Use Up/Down, Ctrl-R, and Right to recall/search/accept history suggestions.
6. Paste the following whole block, press Enter, then evaluate `answer` (expect 6):

   ```python
   def double(x):
       return x * 2
   answer = double(3)
   ```

7. Start `for i in range(2):`, enter an indented print on the next line, then
   finish with an empty line. Ctrl-C cancels unfinished input; Ctrl-D at an empty
   prompt or `exit()` exits. Ctrl-L redraws. History ends with this session.

Automated tests additionally cover pasted conditionals/exception handlers,
completion after reset, plain help output without a pager/global monkeypatch,
wrapped startup text, and redirected input outside the checkout.
