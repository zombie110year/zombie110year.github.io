sync:
	git push origin src
pub:
	git push origin src:release
todo:
	@rg todo
.PHONY: sync pub todo