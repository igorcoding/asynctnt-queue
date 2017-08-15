local function bootstrap()
	local b = {
		tarantool_ver = box.info.version,
		has_new_types = false,
		types = {}
	}

	if b.tarantool_ver >= "1.7.1-245" then
		b.has_new_types = true
		b.types.string = 'string'
		b.types.unsigned = 'unsigned'
		b.types.integer = 'integer'
	else
		b.types.string = 'str'
		b.types.unsigned = 'num'
		b.types.integer = 'int'
	end
	b.types.number = 'number'
	b.types.array = 'array'
	b.types.scalar = 'scalar'
	b.types.any = '*'
	return b
end

_G.B = bootstrap()


box.once('v1', function()
    box.schema.user.create('t1', {password = 't1'})
    box.schema.user.grant('t1', 'read,write,execute', 'universe')
end)

local queue = require('queue')
_G.queue = queue

queue.create_tube('test_tube', 'fifottl', {temporary = true})


function truncate()
    box.space.test_tube:truncate()
end
