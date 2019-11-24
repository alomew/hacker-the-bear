module Main exposing (..)

import Browser
import Element exposing (alignTop, centerX, centerY, column, el, height, padding, row, shrink, spacing, width)
import Element.Font
import Element.Input exposing (labelAbove, labelHidden, labelLeft)
import Html exposing (Html)
import Http
import Json.Decode as Decode exposing (Decoder)
import Json.Encode


main =
    Browser.element { init = init, update = update, view = view, subscriptions = subscriptions }


type alias Model =
    { message : String, queuedMessages : CurrentMessages, summary : String, name : String, user_id : String }


type CurrentMessages
    = Loaded (List String)
    | Loading
    | Failed


type alias Message =
    { message : String, name : String, user_id : String }


encodeMessage : Message -> Json.Encode.Value
encodeMessage message =
    Json.Encode.object <|
        [ ( "message", Json.Encode.string message.message )
        , ( "name", Json.Encode.string message.name )
        , ( "user_id", Json.Encode.string message.user_id )
        ]


encodeModel : Model -> Json.Encode.Value
encodeModel model =
    Json.Encode.object <|
        [ ( "message", Json.Encode.string model.message )
        ]


init : () -> ( Model, Cmd Msg )
init _ =
    ( Model "" Loading "" "" "1"
    , Http.post
        { url = "/getqueuedmessages"
        , body = Http.jsonBody <| Json.Encode.string "1"
        , expect = Http.expectJson ReceivedQueuedMessages (Decode.list Decode.string)
        }
    )


type Msg
    = UpdatedMessage String
    | UpdatedName String
    | Submitted
    | ReceivedSubmitStatus (Result Http.Error Bool)
    | ReceivedQueuedMessages (Result Http.Error (List String))


subscriptions _ =
    Sub.none


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        UpdatedMessage s ->
            ( { model | message = s }, Cmd.none )

        UpdatedName s ->
            ( { model | name = s }, Cmd.none )

        Submitted ->
            ( model
            , Http.post
                { url = "/newmessage"
                , body = Http.jsonBody <| encodeMessage <| Message model.message model.name model.user_id
                , expect = Http.expectJson ReceivedSubmitStatus Decode.bool
                }
            )

        -- Http.post { url = "/addspeech", body = Http.jsonBody <| encodeModel model, expect = Http.expectWhatever Received})
        ReceivedSubmitStatus (Ok True) ->
            ( { model | name = "", message = "" }
            , Http.post
                { url = "/getqueuedmessages"
                , body = Http.jsonBody <| Json.Encode.string "1"
                , expect = Http.expectJson ReceivedQueuedMessages (Decode.list Decode.string)
                }
            )

        ReceivedSubmitStatus _ ->
            ( model, Cmd.none )

        ReceivedQueuedMessages (Ok messages) ->
            ( { model | queuedMessages = Loaded messages }, Cmd.none )

        ReceivedQueuedMessages (Err _) ->
            ( { model | queuedMessages = Failed }, Cmd.none )


view : Model -> Html Msg
view model =
    Element.layout
        [ Element.Font.size 30 ]
        (row [ centerX, centerY, height shrink ]
            [ column [ centerX, width shrink, spacing 15, alignTop ]
                [ el [ Element.Font.size 40, centerX, width shrink ] (Element.text "Messages so far")
                , case model.queuedMessages of
                    Loaded messages ->
                        column [ centerX, width shrink ] <| List.map (\m -> Element.text m) messages

                    Loading ->
                        Element.none

                    Failed ->
                        el [] (Element.text "Couldn't load submitted messages. Maybe refresh.")
                ]
            , column [ width shrink, spacing 15, alignTop ]
                [ Element.Input.text [ centerX, width shrink ] { onChange = UpdatedMessage, text = model.message, placeholder = Nothing, label = labelAbove [] (Element.text "New message") }
                , Element.Input.text [ centerX, width shrink ] { onChange = UpdatedName, text = model.name, placeholder = Nothing, label = labelAbove [] (Element.text "Your name") }
                , Element.Input.button [ centerX, width shrink ] { onPress = Just Submitted, label = Element.text "Submit" }
                ]
            ]
        )
