

d = open("ks_dashboard_gridstack_height_copy.css", "w")
d.write('')
d.close()

f = open("ks_dashboard_gridstack_height_copy.css", "a")
count = 0
px = 45


for count in range(60):
	index = count + 1
	css = """
.grid-stack > .grid-stack-item[data-gs-height='{}'] {{
	height: {}px !important;
}}
.grid-stack > .grid-stack-item[data-gs-min-height='{}'] {{
	min-height: {}px !important;
}}
.grid-stack > .grid-stack-item[data-gs-max-height='{}'] {{
	max-height: {}px !important;
}}
.grid-stack .grid-stack-item[data-gs-y='{}'] {{
  top: {}px !important;
}}
	/************************************ */
	""".format(index,px, index,px, index,px, index,px, index,px)

	f.write(css)
	px += 45
	print(css)
f.close()


