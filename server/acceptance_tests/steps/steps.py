"""Step definitions for acceptance tests"""

@given(u'a variable has been set')
def step_impl(context):
	context.some_var = 'X'

@when(u'the variable is equality checked against itself')
def step_impl(context):
	context.result = context.some_var == context.some_var

@then(u'the expression should return True')
def step_impl(context):
	assert(context.result == True)
