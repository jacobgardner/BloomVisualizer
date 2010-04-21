#include "gameboard.h"
#include <string.h>

#include "visettings.h"

char playerText[][41] = {
  " ______ _       _____   _____________   ",
  " | ___ \\ |     / _ \\ \\ / /  ___| ___ \\  ",
  " | |_/ / |    / /_\\ \\ V /| |__ | |_/ /  ",
  " |  __/| |    |  _  |\\ / |  __||    /   ",
  " | |   | |____| | | || | | |___| |\\ \\   ",
  " \\_|   \\_____/\\_| |_/\\_/ \\____/\\_| \\_|  "
};

char playerOneText[][41] = {
 "                   __                   ",
 "                  /  |                  ",
 "                  `| |                  ",
 "                   | |                  ",
 "                   | |                  ",
 "                  \\___/                 "

};

char playerTwoText[][41] = {
 "                 _____                  ",
 "                / __  \\                 ",
 "                `\' / /\'                 ",
 "                  / /                   ",
 "                ./ /___                 ",
 "                \\_____/                 "
};

char winsText[][41] = {
"      _    _ _____ _   _  _____ _       ",
"     | |  | |_   _| \\ | |/  ___| |      ",
"     | |  | | | | |  \\| |\\ `--.| |      ",
"     | |/\\| | | | | . ` | `--. \\ |      ",
"     \\  /\\  /_| |_| |\\  |/\\__/ /_|      ",
"      \\/  \\/ \\___/\\_| \\_/\\____/(_)      ",
"                                        ",
"       Press Any Key To Continue        ",
"                                        "
};

Gameboard::Gameboard( int x, int y, int width, int height )
: Window( x, y, width, height )
{
  setAttr( boardX, (width-2)/2 );
  setAttr( boardY, (height-2)/2 );

  setupPieces();

}

void Gameboard::setupPieces()
{
  //init_color( COLOR_RED, 0x5C, 0x40, 0x33 );

  init_pair(18, getAttr(selectionF), getAttr( selectionB ) );

  init_pair( PLAYER_1_COLOR, getAttr( p1textF ), getAttr( p1textB ) );
  init_pair( PLAYER_2_COLOR, getAttr( p2textF ), getAttr( p2textB ) );

  init_pair( PLAYER_1_PIECE_COLOR, getAttr( p1pieceF ), getAttr( p1pieceB ) );
  init_pair( PLAYER_2_PIECE_COLOR, getAttr( p2pieceF ), getAttr( p2pieceB ));

  init_pair( INSTRUCTIONS, getAttr( instrF ), getAttr( instrB ) );
  init_pair( BACKGROUND_COLOR, getAttr( backgroundF ), getAttr( backgroundB ) );

  init_pair( DEFAULT_COLOR, getAttr( defaultF ), getAttr( defaultB ) );

  background = ACS_CKBOARD;//ACS_LANTERN;

}

void Gameboard::newState( )
{

  GameState state = *getAttr( state );

  // Bounds check on cursor
  if( getAttr( curX ) < 0 )
    setAttr( curX, 0 );
  if( getAttr( curX ) > (getWidth()-3)/2 )
    setAttr( curX, (getWidth()-3)/2 );
  if( getAttr( curY ) < 0 )
    setAttr( curY, 0 );
  if( getAttr( curY ) > (getHeight()-3)/2 )
    setAttr( curY, (getHeight()-3)/2 );


    // Clear the board

  for( int i = 0; i < getAttr(boardX); i++ )
    for( int j = 0; j < getAttr(boardY); j++ )
    {
      if( getAttr(curX) == i && getAttr(curY) == j && !getAttr( autoEnd ) )
        wattron( mWindow, COLOR_PAIR( 18 ) );
      else
        wattron( mWindow, COLOR_PAIR( BACKGROUND_COLOR ) );

      mvwaddch( mWindow, 1+j*2, 1+i*2, background );
      mvwaddch( mWindow, 1+j*2, 2+i*2, background );
      mvwaddch( mWindow, 2+j*2, 1+i*2, background );
      mvwaddch( mWindow, 2+j*2, 2+i*2, background );

      if( getAttr(curX) == i && getAttr(curY) == j && !getAttr( autoEnd ) )
        wattroff( mWindow, COLOR_PAIR( 18 ) );
      else
        wattroff( mWindow, COLOR_PAIR( BACKGROUND_COLOR ) );
    }

  bool plant = false;

  if( getAttr( autoEnd ) )
    for( std::vector<Plant>::iterator i = state.plants.begin(); i != state.plants.end(); i++ )
    {
      if( !(i->ownerID == getAttr( frameNumber )%2) )
      {
        setAttr(plant, &(*i) );
        plant = true;
        break;
      }

    }

  // Draw them plants.
  for( std::vector<Plant>::iterator i = state.plants.begin(); i != state.plants.end(); i++ )
  {

      if( i->x == getAttr(curX) && i->y == getAttr(curY) && !getAttr( autoEnd ) )
      {
        wattron( mWindow, COLOR_PAIR( 18 ) );
        setAttr( plant, &(*i) );
        plant = true;
      }
      else
        wattron( mWindow, COLOR_PAIR( PLAYER_1_PIECE_COLOR+i->ownerID ) );

      int ch = 0;

      // Health Progression:
      // We can modify these numbers:

      bool dead = false;

      if( i->health >= 20 )
        ch = ACS_S1;
      else if( i->health >= 15 )
        ch = ACS_S3;
      else if( i->health >= 10 )
        ch = ACS_S7;
      else if( i->health >= 5 )
        ch = ACS_S9;
      else if( i->health > 0 )
        ch = '_';
      else
      {

        ch = '\\';
        dead = true;
      }

      wattron( mWindow, A_BOLD );
      mvwaddch( mWindow, i->y*2+2, i->x*2+2, ch );
      wattroff( mWindow, A_BOLD );

      if( dead )
        wattron( mWindow, A_BOLD );

      // Flower
      if( i->flower && !dead )
        ch = 'F';
      else if( dead )
        ch = '\\';
      else
        ch = ' ';
      mvwaddch( mWindow, i->y*2+1, i->x*2+1, ch );

      // Root
      if( i->root && !dead )
        ch = 'R';
      else if( dead )
        ch = '/';
      else
        ch = ' ';
      mvwaddch( mWindow, i->y*2+2, i->x*2+1, ch );

      // Leaves
      if( i->leaf && !dead )
        ch = 'L';
      else if( dead )
        ch = '/';
      else
        ch = ' ';
      mvwaddch( mWindow, i->y*2+1, i->x*2+2, ch );

      if( dead )
        wattroff( mWindow, A_BOLD );

      if( i->x == getAttr(curX) && i->y == getAttr(curY) && !getAttr( autoEnd ) )
        wattroff( mWindow, COLOR_PAIR( 18 ) );
      else
        wattroff( mWindow, COLOR_PAIR( 10 ) );

  }

  if( !plant )
    setAttr( plant, 0 );

  update();

  if( getAttr( turnNumber ) == getAttr( game )->states.size()-1 && getAttr( winAnimation ) )
  {



    if( (getAttr( player1Score ) >= getAttr( player2Score ) || getAttr( player2Plants ) == 0) && getAttr( player1Plants ) > 0 )
      playWinAnim( 1 );
    else
      playWinAnim( 2 );
  }

}

void printC( WINDOW *mWindow, int x, int y, long int CH )
{
  mvwaddch( mWindow, x, y, CH );
}

void Gameboard::playWinAnim( int player )
{
  timeout( 75 );
  int c;

  int offsetY = 8;
  int offsetX = 0;

  wattron( mWindow, COLOR_PAIR(PLAYER_1_PIECE_COLOR+player-1) );
  wattron( mWindow, A_BOLD );

  for( int i = 0; i < 6; i++ )
  {
    for( int j = 0; j < 40; j++ )
    {
      if( playerText[i][j] == 0 )
        break;
      mvwaddch( mWindow, i+1+offsetY, j+1+offsetX, playerText[i][j] );
    }
    update();
    c = getch();
  }

  offsetY += 6;



  for( int i = 0; i < 6; i++ )
  {
    for( int j = 0; j < 40; j++ )
    {

      if( player == 1 )
      {
        if( playerOneText[i][j] == 0 )
          break;

        mvwaddch( mWindow, i+1+offsetY, j+1+offsetX, playerOneText[i][j] );
      } else {
        if( playerTwoText[i][j] == 0 )
          break;
        mvwaddch( mWindow, i+1+offsetY, j+1+offsetX, playerTwoText[i][j] );
      }
    }
    update();
    c = getch();
  }

  offsetY += 6;

  for( int i = 0; i < 9; i++ )
  {
    for( int j = 0; j < 40; j++ )
    {
      if( winsText[i][j] == 0 )
        break;
      mvwaddch( mWindow, i+1+offsetY, j+1+offsetX, winsText[i][j] );
    }
    update();
    c = getch();
  }


  wattroff( mWindow, (PLAYER_1_PIECE_COLOR+player-1) );
  wattroff( mWindow, A_BOLD );
  if( getAttr( autoEnd ) )
    timeout( getAttr( endPause) );
  else
    timeout( -1 );
  c = getch();

  setAttr( frameNumber, getAttr( game )->states.size()-1 );
  setAttr( turnNumber, getAttr( game )->states.size()-1 );
  setAttr( currentMode, 1 );
  setAttr( speed, -1 );

  setAttr( winAnimation, false );

  newState();

  setAttr( done, true );

}

