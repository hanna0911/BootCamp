import { shallowMount } from '@vue/test-utils'
import WelcomePage from '@/components/WelcomePage.vue'
import sinon from "sinon"


describe('WelcomePage.vue', () => {
  const change = sinon.spy();
  const wrapper = shallowMount(WelcomePage, {
    listeners: {
      change
    }
  });
  it("renders welcomepage html", () => {
    expect(wrapper.html()).toMatchSnapshot();
  });
})
