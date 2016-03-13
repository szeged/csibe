function(adopt_subprojects)

    # Add subprojects for CMSIS
    set(NAME "CMSIS")
    if (";${SUBPROJECTS};" MATCHES ";${NAME};")
        list(REMOVE_ITEM SUBPROJECTS ${NAME})
        list(APPEND SUBPROJECTS
                CMSIS/BasicMathFunctions
                CMSIS/CommonTables
                CMSIS/ComplexMathFunctions
                CMSIS/ControllerFunctions
                CMSIS/FastMathFunctions
                CMSIS/FilteringFunctions
                CMSIS/MatrixFunctions
                CMSIS/StatisticsFunctions
                CMSIS/SupportFunctions
                CMSIS/TransformFunctions)
        set(SUBPROJECTS ${SUBPROJECTS} PARENT_SCOPE)
        set(CMSIS_BASE_DIR ${CSiBE_SRC_DIR}/CMSIS PARENT_SCOPE)
    endif()

endfunction(adopt_subprojects)
