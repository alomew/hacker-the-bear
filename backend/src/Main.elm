module Main exposing (..)

import Browser
import Element.Input exposing (labelHidden, labelLeft)
import Html exposing (Html)
import Http
import Json.Encode
import Element exposing (column)

main =
  Browser.element { init = init, update = update, view = view , subscriptions = subscriptions}

type alias Model = {user_id: String, person_text: String, bear_text: String}

encodeModel : Model -> Json.Encode.Value
encodeModel model =
    Json.Encode.object <|
        [ ( "user_id", Json.Encode.string model.user_id )
        , ( "person_text", Json.Encode.string model.person_text )
        , ( "bear_text", Json.Encode.string model.bear_text )
        ]

init : () -> (Model, Cmd Msg)
init _ = (Model "" "" "", Cmd.none)

type Msg
    = UpdatedId String
    | UpdatedPersonText String
    | UpdatedChatText String
    | Submitted
    | Received (Result Http.Error ())

subscriptions _ = Sub.none

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
    case msg of
        UpdatedId newId -> ({model | user_id = newId}, Cmd.none)

        UpdatedPersonText newText -> ({model | person_text = newText}, Cmd.none)

        UpdatedChatText newText -> ({model | bear_text = newText}, Cmd.none)

        Submitted -> (Model "" "" ""
                     , Http.post { url = "/addspeech", body = Http.jsonBody <| encodeModel model, expect = Http.expectWhatever Received})

        Received _ -> (model, Cmd.none)


view : Model -> Html Msg
view model = Element.layout [] (column [] [ Element.Input.text [] {onChange = UpdatedId, text = model.user_id, placeholder = Nothing, label = labelLeft [] (Element.text "ID")}
                                      , Element.Input.text [] {onChange = UpdatedPersonText, text = model.person_text, placeholder = Nothing, label = labelLeft [] (Element.text "Person Text")}
                                      , Element.Input.text [] {onChange = UpdatedChatText, text = model.bear_text, placeholder = Nothing, label = labelLeft [] (Element.text "Bear text")}
                                      , Element.Input.button [] {onPress = Just Submitted, label = Element.text "Submit"}
                                      ])

