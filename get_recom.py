import random
import numpy as np


def choose_recom(type):
  if type=="How-to":
    options={
        1: """We see that there are instructions in your video. Consider 
        adding "chapter break frames" to help show your audience the steps 
        in your process. For example blank frames that read 'Step 1' 'Step 2' 'Step 3'.""",
        2: """It looks like you are showing your viewers how to make something.
         Consider showing the final product in the first 10-seconds to give your 
         viewer an idea of what they will get by the end of the video. This will
          increase the likelyhood that they will finish your video by 25%.""",
        3: """It looks like you are creating a "How To" video. Consider adding a 
        Call-To-Action (CTA) at the end of your video. This gives your viewers someplace
         to learn more and engage with you.""",
         4: """Good job! Are there any parts with no audio that can be sped up to make the video shorter?""",
         5: """Great video! You've put a finished product first, created titles to
          outline your steps and provided great footage. Consider creating a 1 
          minute cutdown to make your how-to even more concise.""",
         6: """This is a great "How To" video! Given most average watch 
         time on YouTube is roughly 8 minutes, consider making your video 
         shorter. What information is non essential to your lesson? Shorter 
         videos increases the likelihood that your viewer will watch the full video. """,
         7: """This is a great video! Your pace, explanation, and CTA are concise and 
         clear. Consider making the video shorter to increase the likelihood that your
          viewer will watch the full video."""

    }

    return options[np.random.randint(1,8)]
  if type == "Review":
    options = {
      1: """This is a great video! Consider adding music to make your video more 
      dynamic. A good jingle evokes an emotional response from your viewers""",
      2: """Looks like a cool product! Consider adding a Call-To-Action (CTA) 
      at the end of your video. This gives your viewers someplace to learn more 
      and engage with you.""",
      3:"""Wow this is a great video! Did you make sure to include a demo or shot 
      of your product? Viewers want to see it in action to understand the benefits.""",
      4:"""Wow - great video! Have you thought about adding customer reviews? Hearing
       from other buyers helps build trust with new potential customers.""",
      5: """Beautiful video! Your b-roll shots are averaging 4 seconds each.
       Consider tightening them up to speed the pace up. """,
      6:"""Don't forget to add closed captions. This is vital for not only 
      compliance purposes but to help viewers fully experience your story.""",
      7: """It's 10 seconds until you start speaking, consider shortening your intro.""",
      8:"""Wow - great video! Where are you sharing it? Given the length of the video 
      consider sharing it on YouTube or your website. """,
      9: """Great use of b-roll! Have you thought about adding an offer to
       your viewers at the end of your video? This could be a discount code or exclusive event invitation."""
    }
    return options[np.random.randint(1,8)]



