sync:
	git push origin src
pub:
	git push origin src:release
todo:
	@rg todo
	@rg 'status: ?draft' posts/
.PHONY: sync pub todo