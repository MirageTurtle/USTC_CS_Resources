FILENAME = hw04
${FILENAME}.pdf: ${FILENAME}.tex
	xelatex $^

clean:
	@mv ${FILENAME}.pdf ../PB19071405_王昊元_${FILENAME}.pdf
	@rm ${FILENAME}.log
	@rm ${FILENAME}.aux
	@rm ${FILENAME}.out