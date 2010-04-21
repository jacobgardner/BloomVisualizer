#include "plantinfo.h"

#include "visettings.h"
#include "legend.h"
#include <stdio.h>
#include <string.h>
#include <cstdlib>
#include <fstream>


Plantinfo::Plantinfo( int x, int y, int width, int height )
  : Window( x, y, width, height )
{


}

#define INFO_PRINT( y, z ) { mvwprintw( mWindow, i++, 2, #y": %d        ", getAttr(plant)->z ); }

void Plantinfo::update()
{

  werase(mWindow);
  box( mWindow, 0, 0 );
  wattron( mWindow, COLOR_PAIR( DEFAULT_COLOR ) );


  if( getAttr(plant) )
  {

    int i = 3;
    if( !getAttr( autoEnd ) )
    {
      mvwprintw( mWindow, 1, 2, "Plant Info" );


      INFO_PRINT( Health, health );
      INFO_PRINT( Root Level, rootLevel );
      INFO_PRINT( Leaf Level, leafLevel );
      INFO_PRINT( Flower Level, flowerLevel );
      INFO_PRINT( Root LvlUp, rootLevelUp );
      INFO_PRINT( Leaf LvlUp, leafLevelUp );
      INFO_PRINT( Flower LvlUp, flowerLevelUp );
    } else {

      std::system( "curl -s 131.151.189.189/api/top > topSeeds " );
      std::ifstream in( "topSeeds", ios::in );
      std::string seed, seeds[3];

      in >> seed;

      int k = 0;
      int start = 0;
      for( int i = 0; i < seed.length(); i++ )
      {
        if( seed[i] == ',' || i == seed.length()-1 )
        {
          seeds[k++] = seed.substr( start, i-start );
          start = i+1;
          if( k == 3 )
            break;
        }
      }

      seeds[2] += seed[seed.length()-1];

      mvwprintw( mWindow, 1, 2, "Top Seeds (pun lol)" );
      mvwprintw( mWindow, i++, 2, "1) %s", seeds[0].c_str() );
      mvwprintw( mWindow, i++, 2, "2) %s", seeds[1].c_str() );
      mvwprintw( mWindow, i++, 2, "3) %s", seeds[2].c_str() );


    }
    // Check if plant is talking
    GameState state = *getAttr( state );
    ++i;
    for( std::vector<Animation *>::iterator j = state.animations.begin(); j != state.animations.end(); j++ )
    {
      if( (*j)->type == TALK )
      {
        if( getAttr( plant )->objectID == ((Talk *)(*j))->plantID )
        {

          char *msg = ((Talk *)(*j))->message;
          bool nLine = false;


          for( int l = 0; l < 28; l++ )
          {
            if( msg[l] == '\n' )
            {
              nLine = true;
            }
          }

          while( strlen( msg ) > 28 || nLine )
          {
            nLine = false;
            char str[29];
            strncpy( str, msg, 28 );
            int n = 28;

            for( int l = 0; l < 28 && l < strlen(msg); l++ )
            {
              if( str[l] == '\n' )
              {

                str[l] = '\0';
                n = l;
                break;
              }

            }
            str[28] = '\0';
            mvwprintw( mWindow, i++, 2, "%s", str );
            msg += n+1;

            for( int l = 0; l < 28; l++ )
            {
              if( msg[l] == '\n' )
              {
                nLine = true;
                break;
              }
            }

          }
          mvwprintw( mWindow, i++, 2, "%s", msg );
        }
      }
    }


  } else {
    if( !getAttr( autoEnd ) )
    {
      mvwprintw( mWindow, 1, 2, "Empty" );
    }
    else
    {
      //
    }
  }

  box( mWindow, 0, 0 );
  wrefresh( mWindow );

}

