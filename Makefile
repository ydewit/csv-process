#FILES=$(pathsubst in/%,out/%,$(wildcard in/*.CSV))
IN_FOLDER=in
IN_FILES=$(wildcard $(IN_FOLDER)/*.csv)

OUT_FOLDER=out
OUT_FILES=$(patsubst $(IN_FOLDER)/%,$(OUT_FOLDER)/%,$(IN_FILES))

PROCESSED_FOLDER=processed
PROCESSED_FILES=$(patsubst $(IN_FOLDER)/%,$(PROCESSED_FOLDER)/%,$(IN_FILES))

process: prepare $(OUT_FILES)

$(IN_FOLDER)/%.csv:
	@mkdir -p $(IN_FOLDER)

$(OUT_FOLDER)/%.csv: $(IN_FOLDER)/%.csv
	@mkdir -p out processed
	@iconv -f ISO-8859-15 -t UTF-8 $< | python scripts/razao.py > $(subst .csv,-processed.csv,$@)
	@[[ -f "$<" ]] && mv $< $(patsubst $(IN_FOLDER)/%,$(PROCESSED_FOLDER)/%,$(subst .csv,-original.csv,$<))
	@echo "$<" --\> "$(subst .csv,-processed.csv,$@)"

prepare:
	@-for f in $(IN_FOLDER)/*; do \
		[[ "$$f" != "$${f// /_}" ]] && mv "$$f" "$${f// /_}"; \
	done || true
	@-for f in $(IN_FOLDER)/*; do \
		[[ "$$f" != "$${f%%.CSV}" ]] && mv "$$f" "$${f%%.CSV}.csv"; \
	done || true

clean:
	@rm -f $(OUT_FOLDER)/*.csv $(PROCESSED_FOLDER)/*.csv $(IN_FOLDER)/*.csv
# convert:
# 	@iconv -f ISO-8859-15 -t UTF-8 $(CSV_FILE) | python razao.py

# listar-contas:
# 	grep -E "[^\(]+\s\(([0-9]+)\)\s+[0-9\.]+" $(CSV_FILE)



