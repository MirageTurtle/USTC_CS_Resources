FILENAME = hw05
${FILENAME}.pdf: ${FILENAME}.tex
	xelatex $^

clean:
	@rm ${FILENAME}.log
	@rm ${FILENAME}.aux
	@mv ${FILENAME}.pdf ../PB19071405_王昊元_${FILENAME}.pdf\