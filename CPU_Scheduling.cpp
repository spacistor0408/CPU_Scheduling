#include <iostream>
#include <stdlib.h>
#include <string>
#include <vector>
#include <fstream>

using namespace std ;

typedef struct process{

    int id ;
    int cpu_burst ;
    int arrival_time ;
    int priority ;

} Process ;


/** The Scanner class is to scan input string user typing.
 *  
 *  The main goal is to recognize tokens from a string
 *  
 *  It include some APIs( e.g. Get(), Peek() ) to provide Paser class identify tokens, 
 *  beside, it also provide API to scan input string.
 *  
*/
class Scanner
{

private:

    string user_input ; // Saving input string from user typing
    string::iterator current_reading_char ; // To point the char address of user input string 

    string current_token ; // Saving current cutting token
    string next_token ; // Saving cutting token

    // To cut tokens from scan input
    string CutToken()
    {
        SkipWhiteSpace() ; // skip all of white space first

        if ( IsAlphabet( *current_reading_char ) ) { return CutIDentity() ; }
        else if ( IsDigit( *current_reading_char ) ) { return CutDigit() ; }
        else if ( IsDelimiter( *current_reading_char ) ) { return CutDelimiter() ; }
        
        return "\0" ;
    }
    
    // To peek the next token, but does not get it
    string PeekNextToken()
    {
        string::iterator temp = current_reading_char ;
        string peekToken = CutToken() ;
        current_reading_char = temp ;
        return peekToken ;
    }

    // Skip all of white space until alphabet or \0
    void SkipWhiteSpace()
    {
        while ( IsWhiteSpace( *current_reading_char ) )
            MoveToNextChar() ;
    }

    // Move iterator of reading to next char
    void MoveToNextChar()
    {
        current_reading_char++ ;
    }

    // Cut IDentity as a token 
    string CutIDentity()
    {
        string buffer( 1, *current_reading_char ) ;
        MoveToNextChar() ;
        Cut_IDentity_BackwardChar( buffer ) ;

        return buffer ;
    }

    // Cut IDentity until encountering NOT_Decimal or Not_Alphabet or Not_Underline
    void Cut_IDentity_BackwardChar( string &buffer )
    {
        while ( IsDigit( *current_reading_char )  ||
                IsAlphabet( *current_reading_char ) ||
                *current_reading_char == '_' )
        {
            buffer += *current_reading_char ;
            MoveToNextChar() ;
        }
    }

    // Cut delimiter as a token 
    string CutDelimiter()
    {
        string buffer( 1, *current_reading_char ) ;
        MoveToNextChar() ;

        if ( IsAssignment() || IsBoolOperator() ) Cut_Delimiter_nextChar( buffer ) ;

        return buffer ;
    }

    // Cut Assignment ":="
    string Cut_Delimiter_nextChar( string &buffer )
    {
        buffer += *current_reading_char ;
        MoveToNextChar() ;
        
        return buffer ;
    }

    // Cut digit as a token may include float case
    string CutDigit()
    {
        string buffer ;
        Cut_Digit_BackwardChar( buffer ) ; 

        if ( IsFloat() ) Cut_Float_BackwardChar( buffer ) ;

        return buffer ;
    }

    // Cut Decimal char until NOT_Decimal or Not_Float
    void Cut_Digit_BackwardChar( string &buffer )
    {
        while ( IsDigit( *current_reading_char ) ) 
        {
            buffer += *current_reading_char ;
            MoveToNextChar() ;
        }
    }

    // Read float char until NOT_Decimal
    void Cut_Float_BackwardChar( string &buffer )
    {
        buffer += *current_reading_char ;
        MoveToNextChar() ;
        Cut_Digit_BackwardChar( buffer ) ;
    }

    // To check whether the token is dot
    bool IsFloat()
    {
        return ( *current_reading_char == '.' && isdigit(*(current_reading_char+1)) ) ;
    }

    // To check whether the token is assignment :=
    bool IsAssignment()
    {
        if ( *(current_reading_char-1) == ':' && *current_reading_char == '=' ) return true ;
        return false ;
    }

    // To check whether the token is Boolaan Operator <> >= <=
    bool IsBoolOperator()
    {
        if ( *(current_reading_char-1) == '<' && *current_reading_char == '>' ) return true ;
        if ( *(current_reading_char-1) == '<' && *current_reading_char == '=' ) return true ;
        if ( *(current_reading_char-1) == '>' && *current_reading_char == '=' ) return true ;
        return false ;
    }

    // To check whether the char is white space
    bool IsWhiteSpace( char ch )
    {
        return ( ch == ' '  ||
                 ch == '\t' ||
                 ch == '\n' ) ;
    }

    // To check whether the char is alphabet
    bool IsAlphabet( char ch )
    {
        return isalpha( ch ) ;
    }

    // To check whether the char is delimiter
    bool IsDelimiter( char ch )
    {
        return ispunct( ch ) ;
    }

    // To check whether the char is decimal
    bool IsDigit( char ch )
    {
        if ( IsFloat() ) return true ;
        return isdigit( ch ) ;
    }

    // To set up iterator of reading input
    void InitialReadingIterator()
    {
        current_reading_char = user_input.begin() ;
    }

public:

    // To scan user input to analysis
    bool ScanInput()
    {
        getline( cin, user_input ) ;
        InitialReadingIterator() ;
    }

    // Get function can provide the current token recognizing correct
    string Get()
    {
        current_token = CutToken() ;
        return current_token ;
    }

    // Peek funtion is to peek next token
    string Peek() 
    {
        next_token = PeekNextToken() ;
        return next_token ;
    }

    // check if is end
    bool IsEND()
    {   
        return ( current_reading_char == user_input.end() ) ;
    }

} ;


class FCFS
{

} ;

class RR
{

} ;

class SRTF
{

} ;

class PPRR
{

} ;

class HRRN
{

} ;



int main()
{

    


}
