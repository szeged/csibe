function(adopt_subprojects)

    # Add subprojects for CMSIS
    set(CMSIS_PROJECT_NAME "CMSIS")
    if (";${SUBPROJECTS};" MATCHES ";${CMSIS_PROJECT_NAME};")
        list(REMOVE_ITEM SUBPROJECTS ${CMSIS_PROJECT_NAME})
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

    # Add subprojects for old CSiBE testbed
    set(OLD_CSIBE_PROJECT_NAME "CSiBE-v2.1.1")
    if (";${SUBPROJECTS};" MATCHES ";${OLD_CSIBE_PROJECT_NAME};")
        list(REMOVE_ITEM SUBPROJECTS ${OLD_CSIBE_PROJECT_NAME})
        list(APPEND SUBPROJECTS
                CSiBE-v2.1.1/bzip2-1.0.2)
        set(SUBPROJECTS ${SUBPROJECTS} PARENT_SCOPE)
        set(OLD_CSIBE_BASE_DIR ${CSiBE_SRC_DIR}/CSiBE-v2.1.1 PARENT_SCOPE)
    endif()

endfunction(adopt_subprojects)
