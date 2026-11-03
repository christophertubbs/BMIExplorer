# Console smoke check

Run `python -m bmi_explorer --no-banner` in the installed environment and paste:

```python
n = 'uniform_2d__value'
u = bmi.get_var_grid(n)
r = bmi.get_var_grid('rectilinear_2d__value')
p = bmi.get_var_grid('points_2d__value')
original = bmi
bmi.get_grid_shape(u, np.empty(2, dtype=np.int32))
bmi.get_grid_x(r, np.empty(4, dtype=np.float64))
bmi.get_grid_x(p, np.empty(6, dtype=np.float64))
bmi.set_value(n, [1.0])
print('recovered', bmi.get_current_time())
print('same model', bmi is original, 'grids', len(explorer.list()))
print(bmi.get_grid_rank(bmi.get_var_grid('scalar__value')))
print(explorer.topology(bmi.get_var_grid('unstructured_mixed__value')))
exit()
```

Expected significant output (traceback paths and prompts vary):

```text
array([3, 4], dtype=int32)
array([100., 102., 107., 115.])
array([ 0.,  2.,  3.,  1., -1.,  1.])
BMITypeError: set_value('uniform_2d__value') expected ...
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
