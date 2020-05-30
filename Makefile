sync:
	git push origin src
pub:
	git push origin src:release
todo:
	@rg todo posts/ pages/
	@rg 'status: ?draft' posts/
.PHONY: sync pub todo