#include <Python.h>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python.hpp>



#include "../visualizer/parser.h"
#include "../visualizer/structures.h"

using namespace boost::python;

std::string hello() {
	return "HELLO WORLD";
}

#define VAR(X, Y) .def_readonly( #X, &Y::X )

std::string getTalk( Talk t )
{
    std::string msg = t.message;
    return msg;
}

std::vector<Talk> getAnims( GameState s )
{
    std::vector<Talk> rAnim;
    for( std::vector<Animation *>::iterator i = s.animations.begin(); i != s.animations.end(); i++ )
    {
        if( (*i)->type == TALK )
            rAnim.push_back( *(Talk*)(*i) );
    }

    return rAnim;
}

BOOST_PYTHON_MODULE( libparsermodule )
{
//	def( "initlibparsermodule", initlibparsermodule );
//	def( "hello", hello );

    def( "parseFile", &parseFile );
    def( "getTalk", &getTalk );
    def( "getAnims", &getAnims );

    class_<Animation>("Animation")
        VAR( type, Animation );

    class_<Talk, bases<Animation> >("Talk", no_init)
        VAR( plantID, Talk )
        VAR( message, Talk );

	class_<Plant>("Plant", no_init)
	    VAR( objectID, Plant )
	    VAR( x, Plant )
	    VAR( y, Plant )
	    VAR( ownerID, Plant )
	    VAR( root, Plant )
	    VAR( leaf, Plant )
	    VAR( flower, Plant )
	    VAR( health, Plant )
	    VAR( rootLevel, Plant )
	    VAR( leafLevel, Plant )
	    VAR( flowerLevel, Plant )
	    VAR( rootLevelUp, Plant )
	    VAR( leafLevelUp, Plant )
	    VAR( flowerLevelUp, Plant )
	    VAR( canAct, Plant );

    class_<GameState>("GameState", no_init)
        VAR( plants, GameState )
        VAR( boardX, GameState )
        VAR( boardY, GameState )
        VAR( gameNumber, GameState )
        VAR( player0Light, GameState )
        VAR( player0Score, GameState )
        VAR( player1Light, GameState )
        VAR( player1Score, GameState )
        VAR( playerID, GameState )        
        VAR( turnNumber, GameState )
        VAR( animations, GameState );
        

    class_<std::vector<Plant> >("PlantVec")
        .def(vector_indexing_suite<std::vector<Plant> >());
        
    class_<std::vector<Animation > > ("AnimationVec")
        .def(vector_indexing_suite<std::vector<Animation> > ());

    class_<std::vector<Talk> > ("TalkVec")
        .def(vector_indexing_suite<std::vector<Talk > > () );


    class_<std::vector<GameState> >("GameVec")
        .def(vector_indexing_suite<std::vector<GameState> >());


	class_<Game>("Game", init<>())
    //	.def_readonly( "winner", &Game::winner )
      .def( "getName", &Game::getName )
	    VAR( winner, Game )
   	  VAR( players, Game )
	    VAR( states, Game );   	    

}
