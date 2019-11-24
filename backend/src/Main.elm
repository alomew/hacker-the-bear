module Main exposing (..)

import Browser
import Element exposing (centerX, column, el, padding, shrink, spacing, width)
import Element.Font
import Element.Input exposing (labelAbove, labelHidden, labelLeft)
import Html exposing (Html)
import Http
import Json.Decode exposing (Decoder)
import Json.Encode


main =
    Browser.element { init = init, update = update, view = view, subscriptions = subscriptions }


type alias Model =
    { message : String, queuedMessages : List String, summary : String, name : String, user_id : String }


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
    ( Model "" [] "" "" "1", Cmd.none )


type Msg
    = UpdatedMessage String
    | UpdatedName String
    | Submitted
    | ReceivedSubmitStatus (Result Http.Error Bool)


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
            ( { model | message = "", queuedMessages = model.message :: model.queuedMessages }
            , Http.post
                { url = "/newmessage"
                , body = Http.jsonBody <| encodeMessage <| Message model.message model.name model.user_id
                , expect = Http.expectJson ReceivedSubmitStatus Json.Decode.bool
                }
            )

        -- Http.post { url = "/addspeech", body = Http.jsonBody <| encodeModel model, expect = Http.expectWhatever Received})
        ReceivedSubmitStatus _ ->
            ( model, Cmd.none )


view : Model -> Html Msg
view model =
    Element.layout
        []
        (column [ centerX, width shrink, spacing 15 ]
            [ el [ Element.Font.size 25, centerX, width shrink, padding 10 ] (Element.text "Messages so far")
            , column [ centerX, width shrink ] <| List.map (\m -> Element.text m) model.queuedMessages
            , Element.Input.text [ centerX, width shrink ] { onChange = UpdatedMessage, text = model.message, placeholder = Nothing, label = labelAbove [] (Element.text "New message") }
            , Element.Input.button [ centerX, width shrink ] { onPress = Just Submitted, label = Element.text "Submit" }
            ]
        )
