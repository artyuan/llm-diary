from llama_index.core import PromptTemplate


instruction_str = """\
        1. When the question is about the date, use the column "date" to filter and bring the information
        1. Convert the query to executable Python code using Pandas.
        2. The final line of code should be a Python expression that can be called with the `eval()` function.
        3. The code should represent a solution to the query.
        4. PRINT ONLY THE EXPRESSION.
        5. Do not quote the expression."""

instruction_str_ner = """\
        1. The column text is the most frequent names,and the columns date, person, time, money, org, product and cardinal
        shows the occurrences of these names
        2. Convert the query to executable Python code using Pandas.
        3. The final line of code should be a Python expression that can be called with the `eval()` function.
        4. The code should represent a solution to the query.
        5. PRINT ONLY THE EXPRESSION.
        6. Do not quote the expression."""

new_prompt = PromptTemplate(
    """\
    You are working with a pandas dataframe in Python.
    The name of the dataframe is `df`.
    This is the result of `print(df.head())`:
    {df_str}

    Follow these instructions:
    {instruction_str}
    Query: {query_str}

    Expression: """
)

context = """Purpose: The primary role of this agent is to assist users by providing accurate 
            information about the recorded daily routine. """